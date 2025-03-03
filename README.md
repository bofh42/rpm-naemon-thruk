# rpm-naemon-thruk
my rpm spec files for [Naemon](https://www.naemon.io/) and [Thruk](https://thruk.org/)

# Description
These spec files are based on [home:naemon - openSUSE Build Service](https://build.opensuse.org/project/show/home:naemon).  
I changed them slightly with the goal to build all rpms with only the spec file and sources from git repos.  
Build and tested for/with [Red Hat Enterprise Linux Server](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux/server) 9
or clones like [AlmaLinux](https://almalinux.org/), [Rocky Linux](https://rockylinux.org/).  

# Build rpms
You can build rpms from just the spec file with `spectool -gf -R <spec>` and `rpmbuild -bb <spec>`.

# Full build cycle
The order of building it matters, because of some BuildRequires.  
For me it looks like this:
```
for i in naemon naemon-core naemon-livestatus naemon-vimvault naemon-selinux \
         gearmand mod_gearman libthruk thruk thruk-selinux ; do
  run-image.sh -o el9 -- ~/build/bin/rbba --repo --source rpmbuild/specs/${i}.spec || break
done
```
But my rbba does lots of things for every spec file in a special prepared container
- `createrepo` for `%{_rpmdir}` and `%{_srcrpmdir}`
- setup a local `/etc/yum.repos.d/rpmbuild.repo` pointing there
- `spectool -gf -R <spec>`
- `sudo yum-builddep -y <spec>`
- `rpmbuild -ba <spec>`
```
